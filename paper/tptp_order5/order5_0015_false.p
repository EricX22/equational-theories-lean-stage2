% order5_0015  eq1=32919 eq2=14795  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(f(f(Y,Z),Z),X)),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(f(Y,Z),f(Y,Z)),X)) )).

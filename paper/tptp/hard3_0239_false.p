% hard3_0239  eq1=2156 eq2=1887  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Y),Z),f(W,X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(Y,f(X,X)),f(Y,X)) )).

% order5_0054  eq1=2150 eq2=32872  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Y),Z),f(Y,Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(f(f(Y,Y),Z),Y)),X) )).

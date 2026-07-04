% order5v2_1772  eq1=19884 eq2=15337  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,X),f(f(Z,f(X,X)),W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(X,f(f(f(Y,f(Y,Z)),Z),Y)) )).

% order5_0117  eq1=5372 eq2=1869  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Z,f(Z,f(Y,f(X,Y))))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(Y,Z)),f(X,Z)) )).

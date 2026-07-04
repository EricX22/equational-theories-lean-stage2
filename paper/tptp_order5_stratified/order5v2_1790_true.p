% order5v2_1790  eq1=13325 eq2=30567  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,f(X,X))),Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Y,f(f(Z,X),Z))),W) )).

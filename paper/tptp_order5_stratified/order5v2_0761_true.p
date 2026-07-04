% order5v2_0761  eq1=37418 eq2=415  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(X,f(Y,Z))),W),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(X,f(X,f(Y,Z)))) )).

% order5_0093  eq1=13422 eq2=41254  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,f(W,U))),X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(f(Y,Z),Y),Y),X),W) )).

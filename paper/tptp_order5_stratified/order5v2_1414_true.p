% order5v2_1414  eq1=40593 eq2=41123  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,W)),W),X),U) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(f(Y,Y),Z),Z),Z),Y) )).

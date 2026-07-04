% order5v2_0969  eq1=40964 eq2=24764  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(f(Y,X),Z),Z),X),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(f(Y,Z),W)) )).

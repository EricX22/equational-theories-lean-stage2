% hard3_0097  eq1=752 eq2=2554  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(X,W),X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(f(Y,Z),Y)),X) )).

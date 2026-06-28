% hard3_0363  eq1=3502 eq2=4109  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(f(Z,Z),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(f(Y,Z),Z),Y) )).

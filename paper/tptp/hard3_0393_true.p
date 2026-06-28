% hard3_0393  eq1=4414 eq2=4623  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,f(X,Y)) = f(f(Y,Z),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,X),Y) = f(f(Z,Z),W) )).

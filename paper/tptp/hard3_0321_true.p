% hard3_0321  eq1=2985 eq2=1374  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,X)),W),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,Y),Z),X)) )).

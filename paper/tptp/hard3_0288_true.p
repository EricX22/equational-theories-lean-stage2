% hard3_0288  eq1=2690 eq2=2870  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Z,Z)),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,f(Y,X)),Z),Z) )).
